const EMPTY_PERSON={name:'',email:'',phone:'',maxEdu:'',firstEdu:'',
            quali:0,birth:'',sex:'M',expSalary:0,cmt:'',marriage:'UN'};
export default {
inject:['service', 'tags', 'ibf'],
data() {return {
    list:[], //人才列表
    search:'',
    ctrl:{cur:1,max:0,dlg:false},
    perInfo:{},
    opts:{edu:[],marriage:[]}
}},
created(){
    copyObjTo(EMPTY_PERSON,this.perInfo);
    var pg=this.ibf.getRt('pg', 1);
    this.query(pg);
    var opts=[];
    for(var i in this.tags.edu) {
        opts.push({value:i,label:this.tags.edu[i]});
    }
    this.opts.edu=opts;
    opts=[];
    for(var i in this.tags.marriageSta) {
        opts.push({value:i,label:this.tags.marriageSta[i]});
    }
    this.opts.marriage=opts;
},
methods:{
fmt_lines(data) {
    var dt=new Date();
    var year=dt.getFullYear();
    var list=[];
    var p; //人才
    var cols=data.cols;
    var rows=data.list;
    //quali,sex,birth,expSalary,state,maxEdu,firstEdu,name,phone,email,cmt,createAt
    for(var row of rows) {
        p={};
        for(var i in cols) {
            p[cols[i]]=row[i];
        }
        p.sex_s=this.tags.sex[p.sex];
        p.state=this.tags.perState[p.state];
        p.maxEdu_s=this.tags.edu[p.maxEdu];
        p.firstEdu_s=this.tags.edu[p.firstEdu];
        dt.setTime(p.birth*60000);
        p.age=year-dt.getFullYear();
        p.birth_s=date2str(dt);
        dt.setTime(p.createAt*60000);
        p.createAt_s=date2str(dt);
        dt.setTime(p.update_time);
        p.updateAt=date2str(dt);
        list.push(p);
    }
    this.list=list;
},
query(pg) {
    this.ibf.setRt('pg',pg);
    this.search='';
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var url = "/api/pool/list?offset="+offset+"&num="+this.service.N_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK || resp.data.total==0) {
            this.list=[];
            this.ctrl.max=0;
            this.ctrl.cur=1;
            return;
        }
        this.fmt_lines(resp.data);
        this.ctrl.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
doSearch() {
    if(this.search=='') {
        this.query(this.ibf.getRt('pg', 1));
        return;
    }
    var url="/api/pool/search?s="+this.search+"&limit="+this.service.N_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            return;
        }
        this.fmt_lines(resp.data);
        this.ctrl.max=1;
    })
},
showCreate() {
    copyObjTo(EMPTY_PERSON, this.perInfo);
    this.ctrl.dlg=true;
},
create() {
    var dta=copyObjExc(this.perInfo,['uid','birth']);
    var url="/api/pool/add";
    dta.birth=parseInt(new Date(this.perInfo.birth).getTime()/60000);
    
    request({method:"POST",url:url,data:dta}, this.service.name).then(resp => {
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.ctrl.dlg=false;
        this.query(this.ctrl.cur);
    });
},
detail(id) {
    this.service.goto("/person?uid="+id);
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat icon="arrow_back" dense @click="service.back"></q-btn>
    <q-toolbar-title>{{tags.pool.title}}</q-toolbar-title>
  </q-toolbar>
  </q-header>
  <q-footer class="bg-white q-pa-md">
    <q-input outlined v-model="search" :label="tags.search" dense @keyup.enter="doSearch">
     <template v-slot:append>
      <q-icon v-if="search!==''" name="close" @click="query(1)" class="cursor-pointer"></q-icon>
      <q-icon name="search" @click="doSearch"></q-icon>
     </template>
     <template v-slot:after>
      <q-btn round color="primary" icon="add_circle" @click="showCreate"></q-btn>
     </template>
    </q-input>
  </q-footer>
  <q-page-container>
    <q-page class="q-pa-md">
<div class="q-pa-sm flex flex-center" v-show="ctrl.max>1">
 <q-pagination v-model="ctrl.cur" color="primary" :max="ctrl.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query"></q-pagination>
</div>
<q-list separator>
 <q-item>
  <q-item-section><q-item-label caption>{{tags.pub.name}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.pub.contact}}</q-item-label></q-item-section>
  <q-item-section side><q-item-label caption>{{tags.pub.ability}}</q-item-label></q-item-section>
 </q-item>
 <q-item v-for="p in list" @click="detail(p.uid)" clickable>
  <q-item-section>
   <q-item-label>{{p.name}} {{p.sex_s}} {{p.age}}{{tags.age}}</q-item-label>
   <q-item-label caption>{{p.createAt_s}} {{p.state}}</q-item-label>
   <q-item-label caption>{{p.updateAt}}</q-item-label>
  </q-item-section>
  <q-item-section>
   <q-item-label>{{p.phone}}</q-item-label>
   <q-item-label caption>{{p.email}}</q-item-label>
  </q-item-section>
  <q-item-section side>
   <q-item-label caption>{{p.cmt}}</q-item-label>
   <q-item-label caption>{{p.quali}}/{{p.expSalary}}</q-item-label>
   <q-item-label caption>{{p.maxEdu_s}}/{{p.firstEdu_s}}</q-item-label>
  </q-item-section>
 </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="ctrl.dlg">
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{tags.add}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
     <q-list>
      <q-item><q-item-section>
       <q-input v-model="perInfo.name" :label="tags.pub.name" dense maxlength=80>
        <template v-slot:after>
         <q-radio v-model="perInfo.sex" class="text-caption"
         v-for="(s,v) in tags.sex" :val="v" :label="s"></q-radio>
        </template>
       </q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-select v-model="perInfo.maxEdu" :options="opts.edu" emit-value
        :label="tags.employee.maxEdu" dense map-options></q-select>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-select v-model="perInfo.firstEdu" :options="opts.edu" emit-value
        :label="tags.employee.firstEdu" dense map-options></q-select>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-input v-model.number="perInfo.quali" :label="tags.employee.quali" dense type="number"></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-input v-model.number="perInfo.expSalary" :label="tags.pool.expSalary" dense type="number"></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-input v-model.number="perInfo.phone" :label="tags.pub.phone" dense maxlength=90 type="number"></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <date-input :close="tags.ok" :label="tags.pub.birth"
        v-model="perInfo.birth" max="today"></date-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-select v-model="perInfo.marriage" :options="opts.marriage" emit-value
        :label="tags.pool.marriage" dense map-options></q-select>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-input v-model="perInfo.email" :label="tags.pub.email" dense maxlength=80></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-input v-model="perInfo.cmt" :label="tags.pool.cmt" dense maxlength=500></q-input>
      </q-item-section></q-item>
     </q-list>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.ok" color="primary" @click="create"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
`
}