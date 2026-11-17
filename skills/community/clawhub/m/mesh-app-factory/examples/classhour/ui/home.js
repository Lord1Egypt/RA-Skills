export default {
inject:['service', 'tags'],
data() {return {
    isOwner:false,
    students:[], //学员列表
    search:'',
    studentPg:{cur:1,max:0,searchTag:''},
    newStudent:{name:'',mobile:'',sex:'',birth:'',points:0},
    newConsume:{pkgId:0,val:'',students:{},comment:'',point:'',percent:0,msg:''},
    dlgs:{student:false,consume:false,packages:[],packageOpts:[]},
    stuOpts:{opts:[],//供选择的学员列表
        values:null //选中项，不能赋值[]，会显示一个空选项
    }
}},
created(){
    var url="/power/get?service="+this.service.name;
    request({method:"GET",url:url}, SERVICE_USER).then(resp => {
        if(resp.code!=0) {
            Console.warn("request "+url+" failed:" + resp.code + ",info:" + resp.info);
            return;
        }
        this.isOwner=resp.data.role=='admin';
    }); 
    this.query_students(0);
},
methods:{
query_students(offset) {
    this.search="";
    var url="/api/student/list?offset="+offset+"&num="+this.service.NUM_PER_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.students=[];
            this.studentPg.max=0;
            this.studentPg.searchTag=this.tags.search;
        } else {
            this.formatData(resp.data.students);
            this.studentPg.max=Math.ceil(resp.data.total/this.service.NUM_PER_PAGE);
            this.studentPg.searchTag=this.tags.search + '(' + resp.data.total + ')';
        }
    })
},
search_students() {
    if(this.search=='') {
        this.query_students(0);
        return;
    }
    var url="/api/student/search?s="+this.search+"&limit="+this.service.NUM_PER_PAGE
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.formatData(resp.data.students);
        this.studentPg.max=1;
    })
},
formatData(rows) {
    var students=[];
    var dt=new Date();
    var updateAt, birth, age;
    var nowYear=dt.getFullYear();
    for(var r of rows) {
        dt.setTime(r.update_time);
        updateAt=dt.toLocaleDateString();
        dt.setTime(r.birth*86400000);
        birth=dt.toLocaleDateString();
        age=nowYear-dt.getFullYear();
        students.push({id:r.id, name:r.name,points:r.points,sex:this.tags.sexInfo[r.sex].n,
        updateAt:updateAt,birth:birth,age:age});
    }
    this.students=students;
},
add_student() {
    var url="/api/student/add";
    var d=this.newStudent;
    var birth=new Date(d.birth).getTime()/86400000;
    var reqDta={name:d.name,mobile:d.mobile,sex:d.sex,birth:birth,points:d.points}
    request({method:"POST",url:url,data:reqDta}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.dlgs.student=false;
        this.query_students(0);
    })
},
change_student_page(page) {
    this.query_students((parseInt(page)-1)*this.service.NUM_PER_PAGE);
},
open_create_consume(student){
    this.newConsume.val='';
    this.newConsume.students={};
    this.newConsume.point='';
    this.newConsume.comment='';
    this.newConsume.msg='';
    this.newConsume.percent=0;
    this.stuOpts.opts=[];
    this.stuOpts.values=null;
    this.service.getPackages().then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, [resp.info, this.tags.nodlgs.packages]);
            return;
        }
        this.dlgs.packages=resp.pkgs;
        this.dlgs.packageOpts=resp.opts;
        var pkg=this.dlgs.packages[0];
        this.newConsume.pkgId=pkg.id;
        this.dlgs.consume=true;
    }).catch(err=>{
        Console.info(err);
    });
},
create_consumes(){
    var c=this.newConsume;
    if(Object.keys(c.students).length==0) {//{id:name}
        return; //没有选定学员，不做任何操作
    }
    var students=[];
    for(var stu in c.students) {
        students.push(parseInt(stu));
    }
    var progressStep=1.0/students.length;
    var reqDta={students:students,pkgId:c.pkgId,val:c.val};
    request({method:"POST",url:"/api/consume/getOrders",data:reqDta}, this.service.name).then(resp=>{
        var orders={};
        var num=0;
        if(resp.code == RetCode.OK) {
            for(var ord of resp.data.list) {//id,balance,student
              var stu=ord.student;
              if(!orders[stu]) {//可能存在多个订单，已经有了，不必再插入
                orders[stu]={order:ord.id,balance:ord.balance};
                num++;
              }
            }
        }
        
        if(num!=students.length) {
            var msg="";
            for(var stu of students) {
                if(!orders[stu]) {
                    if(msg!='') {
                        msg += ",";
                    }
                    msg += c.students[stu];
                }
            }
            this.newConsume.msg=this.tags.noBalance + ":" + msg;
            return;
        }
        c.percent=0.1; //显示进度条
        
        var url="/api/consume/create";
        for(var stu in c.students) {
            var reqData={order:orders[stu].order,val:c.val,student:stu,comment:c.comment,point:c.point};
            request({method:"POST",url:url,data:reqData}, this.service.name).then(resp=>{
                if(resp.code != RetCode.OK) {
                    if(msg!='') {
                        msg += ",";
                    }
                    msg += this.newConsume.students[stu].name;
                }
                c.percent+=progressStep;
                if(c.percent>=1.0) {
                    this.dlgs.consume=false;
                    this.$refs.errMsg.show(this.tags.oprSuccess);
                }                
            })
        }
    })
},
//处理学员选择的三个函数
filter_student(val,update) {
  if(val==='') {
    update(() => {
      this.stuOpts.opts=[]
    })
    return;
  }
  update(() => {
    var url="/api/student/search?s="+val+"&limit="+this.service.NUM_PER_PAGE
    request({method:"GET",url:url}, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.stuOpts.opts=[]
            return;
        }

        var opts=[];
        for(var stu of resp.data.students) {
            opts.push({value:stu.id, label:stu.name});
        }
        this.stuOpts.opts=opts;
    })
  })    
},
input_student(val, done) {
  if (val.length > 0) {
     done(val, 'add-unique')
  }
},
student_changed() {
    this.newConsume.students={}
    for(var c of this.stuOpts.values) {
        this.newConsume.students[c.value]=c.label;
    }
}
},

template:`
<q-layout view="hHh lpr fFf">
  <q-header class="bg-grey-1 text-primary" elevated>
   <q-toolbar>
    <q-avatar square><img src="./favicon.png"></q-avatar>
    <q-toolbar-title>{{tags.app_name}}</q-toolbar-title>
   </q-toolbar>
  </q-header>
  <q-footer class="bg-white q-pa-md">
    <q-input outlined v-model="search" :label="studentPg.searchTag" dense @keyup.enter="search_students">
    <template v-slot:append>
      <q-icon name="close" v-show="search!==''" @click="query_students(0)" class="cursor-pointer q-mr-md"></q-icon>
    </template>
    <template v-slot:after>
      <q-btn icon="search" round color="secondary" @click="search_students"></q-btn>
    </template>
    </q-input>
  </q-footer>
  <q-page-container>
    <q-page class="q-pa-md">
<div class="q-pa-lg flex flex-center" v-if="studentPg.max>1">
 <q-pagination v-model="studentPg.cur" color="primary" :max="studentPg.max" max-pages="10"
  boundary-numbers="false" @update:model-value="change_student_page"></q-pagination>
</div>

<q-markup-table flat>
 <thead><tr>
  <th class="text-left">{{tags.student}}</th>
  <th class="text-right">{{tags.points}}</th>
  <th class="text-right">{{tags.updateAt}}</th>
 </tr></thead>
 <tbody>
 <tr v-for="v in students" @click="service.jumpTo('/student?id='+v.id)">
  <td class="text-left">
   <list dense><q-item-section>
    <q-item-label>{{v.name}}({{v.sex}},{{v.age}})</q-item-label>
    <q-item-label caption>{{tags.birth}}:{{v.birth}}</q-item-label>
   </q-item-section></list>
  </td>
  <td class="text-right">{{v.points}}</td>
  <td class="text-right">{{v.updateAt}}</td>
 </tr>
 </tbody>
</q-markup-table>

<q-page-sticky position="bottom-right" :offset="[20,20]">
 <q-fab icon="construction" color="primary" direction="up" padding="1em">
  <q-fab-action color="primary" icon="person_add" :label="tags.addVip" external-label label-position="left"
   @click="newStudent={name:'',mobile:'',sex:'F'};dlgs.student=true;"></q-fab-action>
  <q-fab-action color="primary" icon="payment" :label="tags.addConsume" external-label label-position="left"
   @click="open_create_consume"></q-fab-action>
  <q-fab-action v-if="isOwner" color="accent" icon="settings" external-label label-position="left"
   @click="service.jumpTo('/settings')" :label="tags.settings"></q-fab-action>
  <q-fab-action v-if="isOwner" color="accent" icon="bar_chart" external-label label-position="left"
   @click="service.jumpTo('/reports')" :label="tags.reports"></q-fab-action>
 </q-fab>
</q-page-sticky>
    </q-page>
  </q-page-container>
</q-layout>
    
<q-dialog v-model="dlgs.student">
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{tags.addVip}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
     <q-input v-model="newStudent.name" :label="tags.name" dense
     :rules="[v=>v!=''|| tags.namePls]"></q-input>
     <q-input v-model="newStudent.mobile" :label="tags.mobile" maxlength=11
     :rules="[v=>/^1[0-9]{10}$/.test(v)|| tags.mobilePls]" dense></q-input>
     <component-date-input :close="tags.ok" :label="tags.birth" v-model="newStudent.birth" max="today"></component-date-input>
     <q-input v-model="newStudent.points" :label="tags.points" dense type="number"></q-input>
     <div class="q-gutter-sm">
      <q-radio v-model="newStudent.sex" val="F" :label="tags.sexInfo.F.n"></q-radio>
      <q-radio v-model="newStudent.sex" val="M" :label="tags.sexInfo.M.n"></q-radio>
     </div>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn flat :label="tags.ok" color="primary" @click="add_student"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<q-dialog v-model="dlgs.consume">
 <q-card style="min-width:70vw">
  <q-card-section><div class="text-h6">{{tags.addConsume}}</div></q-card-section>
  <q-card-section class="q-pt-none">
    <q-select v-model="newConsume.pkgId" emit-value map-options
     :options="dlgs.packageOpts" @update:model-value="pkg_changed"></q-select>
    <q-select v-model="stuOpts.values" :label="tags.student" :options="stuOpts.opts"
      use-input use-chips multiple
      hide-dropdown-icon input-debounce=200 dense
      @new-value="input_student" @filter="filter_student"
      @update:model-value="student_changed">
     <template v-slot:selected-item="scope">
      <q-chip removable dense @remove="scope.removeAtIndex(scope.index)"
        :tabindex="scope.tabindex" class="q-ma-none">
        {{scope.opt.label}}
      </q-chip>
     </template>
    </q-select>
    <q-input v-model="newConsume.val" :label="tags.consumeVal" dense
     :rules="[v=>/^[0-9]+(.[0-9]{1,2})?$/.test(v)|| tags.numberPls]"></q-input>
    <q-input v-model="newConsume.point" :label="tags.consumePoint" type="number"></q-input>
    <q-input v-model="newConsume.comment" :label="tags.comment" dense
     type="textarea" autogrow></q-input>
  </q-card-section>
  <q-linear-progress v-show="newConsume.percent>0" stripe rounded size="20px"
  :value="newConsume.percent" color="warning" class="q-mt-sm"></q-linear-progress>
  <q-card-section class="q-pt-none text-red">{{newConsume.msg}}</q-card-section>
  <q-card-actions align="right">
     <q-btn flat :label="tags.ok" color="primary" @click="create_consumes"></q-btn>
     <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></component-alert-dialog>
`
}