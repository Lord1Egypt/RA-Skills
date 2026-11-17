import {sta2icon} from '/assets/v3/components/workflow.js';
export default {
inject:['service', 'tags'],
data() {return {
    uid:this.$route.query.uid,
    event:{cur:1,max:0,list:[]},
    workflow:{cur:1,max:0,list:[]},
    signer:[], //权签人，离职、调薪、调股份等用到

    empInfo:{uid:this.$route.query.uid,
        office:0,worktime:0,stock:0,quali:'',post:'',attend:'',
        salary:'',dSalary:'',hSalary:'',subsidy:'',entryAt:'',
        account:'',addr:'',email:'',idno:'',state:'NORM',
        holiday:0,weal:0,sickRatio:0,
        rList:[] //挂账资产列表
    },
    ctrl:{ei:{},weal:false,zone:false},
    opts:{zone:[],office:[],worktime:[]},
    leave:{dlg:false, disable:false, state:'LEAV', cmt:''},
    grade:{dlg:false,post:0,quali:0,subsidy:0,cmt:''},
    stock:{dlg:false,stock:0,cmt:''},
    salary:{dlg:false,salary:0,dSalary:0,hSalary:0,cmt:''}
}},
created(){
    this.service.worktimeList().then(opts=>{
        this.opts.worktime=opts;
    });
    this.service.zoneList().then(opts=>{
        this.opts.zone=opts;
    });
    this.service.allOffices().then(()=> {
        this.get();
    }); //生成officeMap
    this.getEvents(1);
    this.getWorkflows(1);
},
methods:{
get() {
    var url = "/api/employee/get?uid="+this.uid;
    request({method:"GET",url:url}, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            return;
        }
        this.empInfo=this.convert(resp.data);
        //已提出离职的，不能再提出离职
        this.empInfo.showLeave=this.uid>1&&'leave'!=resp.data.recentFlow;
    })
},
convert(src) {
    var dt=new Date();
    var year=dt.getFullYear();
    var p={};
    copyObjTo(src, p);
    p.uid=this.uid;
    p.sex_s=this.tags.sex[p.sex];
    p.state_s=this.tags.empState[p.state];
    p.state_b=p.state=='NORM';
    p.maxEdu_s=this.tags.edu[p.maxEdu];
    p.firstEdu_s=this.tags.edu[p.firstEdu];
    dt.setTime(p.birth*60000);
    p.age=year-dt.getFullYear();
    dt.setTime(p.entryAt*60000);
    p.entryAt_s=date2str(dt);
    p.worktime_s=this.service.worktimeMap[p.worktime];
    p.office_s=this.service.officeMap[p.office];
    return p;
},
getEvents(pg) {
    var pgSize=this.service.N_SMPG;
    var offset=(parseInt(pg)-1)*pgSize;
    var url = "/api/event/list?uid="+this.uid+"&offset="+offset+"&num="+pgSize;
    request({method:"GET",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            return;
        }
        var dt=new Date();
        //at,type,val,cmt,cfmAcc
        this.event.list=resp.data.list.map(e => {
            dt.setTime(e.at*60000);
            e.at=date2str(dt);
            e.type_s=this.tags.evtType[e.type];
            return e;
        });
        this.event.max=Math.ceil(resp.data.total/pgSize);
    })
},
getWorkflows(pg) {
    var pgSize=this.service.N_SMPG;
    var offset=(parseInt(pg)-1)*pgSize;
    var url = "/api/wfemployee/list?uid="+this.uid+"&offset="+offset+"&num="+pgSize;
    request({method:"GET",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            return;
        }
        var dt=new Date();
        //flowid,did,flSta,createAt,name
        this.workflow.list=resp.data.list.map(e => {
            dt.setTime(e.createAt*60000);
            e.createAt=date2str(dt);
            e.staIcon=sta2icon(e.flSta);
            return e;
        });
        this.workflow.max=Math.ceil(resp.data.total/pgSize);
    })
},
doLeave() { //离职
    var url="/api/wfemployee/leave";
    var dta=copyObjExc(this.leave, ["dlg","disable"]);
    dta.uid=this.uid;
    dta.signer=this.signer.account;
    request({method:"PUT", url:url, data:dta}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.leave.dlg=false;
    });
},
showLeave() {
    if(!this.empInfo.showLeave)return;
    var url = "/api/resource/list?uid="+this.uid;
    request({method:"GET",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.empInfo.rList=[];
        } else {
            var dt=new Date();
            this.empInfo.rList=resp.data.list.map(l=>{
                dt.setTime(l.start*60000);
                l.start=date2str(dt);
                dt.setTime(l.inDate*60000);
                l.inDate=date2str(dt);
                return l;
            });
        }
        this.leave.disable=this.empInfo.rList.length>0; //挂了资产，离职前必须先清退
        this.leave.dlg=true;
    });
},
toggleHide() {
    var state;
    if(this.empInfo.state=='HIDE') {
        state='NORM';
    } else if(this.empInfo.state=='NORM') {
        state='HIDE';
    } else {
        return;
    }
    var url="/api/employee/toggleHide";
    var dta={uid:this.uid,state:state};
    request({method:"PUT", url:url, data:dta}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.empInfo.state_b=(this.empInfo.state=='NORM');
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.empInfo.state=state;
        this.empInfo.state_s=this.tags.empState[state];
        this.empInfo.state_b=(state=='NORM');
    });
},
changeOffice(zone) {
    this.service.officeList(zone).then(opts=>{
        this.opts.office=opts;
    });
},
modifyZone() {
    var url="/api/employee/setZone";
    var dta={uid:this.uid,office:this.empInfo.office,worktime:this.empInfo.worktime};
    request({method:"PUT", url:url, data:dta}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.empInfo.worktime_s=this.service.worktimeMap[this.empInfo.worktime];
        this.empInfo.office_s=this.service.officeMap[this.empInfo.office];
        this.ctrl.zone=false;
    });
},
showGrade() {
    this.grade.post=this.empInfo.post;
    this.grade.quali=this.empInfo.quali;
    this.grade.subsidy=this.empInfo.subsidy;
    this.grade.cmt='';
    this.grade.dlg=true;
},
modifyGrade() {
    var url="/api/wfemployee/setGrade";
    var dta=copyObjExc(this.grade, ["dlg"]);
    dta.uid=this.uid;
    dta.signer=this.signer.account;
    request({method:"PUT", url:url, data:dta}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.grade.dlg=false;
        this.getWorkflows(this.workflow.cur);
    });
},
showSalary() {
    this.salary.salary=this.empInfo.salary;
    this.salary.dSalary=this.empInfo.dSalary;
    this.salary.hSalary=this.empInfo.hSalary;
    this.salary.cmt='';
    this.salary.dlg=true;
},
modifySalary() {
    var url="/api/wfemployee/setSalary";
    var dta=copyObjExc(this.salary, ["dlg"]);
    dta.uid=this.uid;
    dta.signer=this.signer.account;
    request({method:"PUT", url:url, data:dta}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.salary.dlg=false;
        this.getWorkflows(this.workflow.cur);
    });
},
showStock() {
    this.stock.stock=this.empInfo.stock;
    this.stock.cmt='';
    this.stock.dlg=true;
},
modifyStock() {
    var url="/api/wfemployee/setStock";
    var dta=copyObjExc(this.stock, ["dlg"]);
    dta.uid=this.uid;
    dta.signer=this.signer.account;
    request({method:"PUT", url:url, data:dta}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.stock.dlg=false;
        this.getWorkflows(this.workflow.cur);
    });
},
modifyWeal() {
    var url="/api/employee/setWeal";
    var dta={uid:this.uid,
        holiday:this.empInfo.holiday,
        weal:this.empInfo.weal,
        sickRatio:this.empInfo.sickRatio};
    request({method:"PUT", url:url, data:dta}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.ctrl.weal=false;
    });
},
cfmEvent(at,type) {
    var url="/api/event/confirm";
    var dta={uid:this.uid,at:at,type:type};
    request({method:"PUT", url:url, data:dta}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.getEvents(this.event.cur);
    }); 
},
salaryChange(v) {
    this.salary.dSalary=parseInt(v/22);
    this.salary.hSalary=parseInt(v/(22*8));
},
showFlow(flowid,did,name) {
    var url='/workflow?flow='+flowid+"&did="+did+"&type="+name;
    this.service.goto(url);
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat icon="arrow_back" dense @click="service.back"></q-btn>
    <q-toolbar-title>{{tags.employee.detail}}-{{empInfo.name}} {{empInfo.sex_s}}</q-toolbar-title>
    <q-btn flat dense :label="tags.employee.leave" @click="showLeave" v-if="empInfo.showLeave"></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
<q-list dense>
  <q-item>
   <q-item-section>{{tags.employee.maxEdu}}/{{tags.employee.firstEdu}}</q-item-section>
   <q-item-section><div>
    {{empInfo.maxEdu_s}}/{{empInfo.firstEdu_s}}
    <q-badge color="primary" @click="service.goto('/ibf/resume?uid='+uid)">
     {{tags.employee.resume}}<q-icon name="event_note" color="white"></q-icon>
    </q-badge>
   </div></q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.employee.addr}}</q-item-section>
   <q-item-section>{{empInfo.addr}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.pub.phone}}</q-item-section>
   <q-item-section>{{empInfo.phone}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.pub.email}}</q-item-section>
   <q-item-section>{{empInfo.email}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.employee.state}}</q-item-section>
   <q-item-section>
    <q-toggle v-model="empInfo.state_b" :label="empInfo.state_s"
    @update:model-value="toggleHide" dense
    unchecked-icon="visible_off" checked-icon="visible"></q-toggle>
   </q-item-section>
  </q-item>
</q-list>
<q-separator inset></q-separator>
<q-list dense v-if="!ctrl.zone">
  <q-item>
   <q-item-section>
    <q-item-label caption>{{tags.employee.office}}:{{empInfo.office_s}}</q-item-label>
    <q-item-label caption>{{tags.employee.worktime}}:{{empInfo.worktime_s}}</q-item-label>
   </q-item-section>
   <q-item-section avatar>
    <q-icon name="edit" flat color="primary"
    @click="ctrl.zone=true;changeOffice(empInfo.zone);"></q-btn>
   </q-item-section>
  </q-item>
</q-list>
<q-list dense v-else>
  <q-item>
   <q-item-section>
    <q-select v-model="empInfo.zone" :options="opts.zone" @update:model-value="changeOffice"
     :label="tags.employee.zone" dense map-options emit-value></q-select>
     <q-select v-model="empInfo.office" :options="opts.office"
     :label="tags.employee.office" dense map-options emit-value></q-select>
    <q-select v-model="empInfo.worktime" :options="opts.worktime" emit-value
     :label="tags.employee.worktime" dense map-options></q-select>
   </q-item-section>
   <q-item-section avatar>
    <q-btn icon="cancel" @click="ctrl.zone=false" flat color="primary"></q-btn>
    <q-btn icon="done" @click="modifyZone" flat color="primary"></q-btn>
   </q-item-section>
  </q-item>
</q-list>
<q-separator inset></q-separator>
<q-list dense v-if="!ctrl.weal">
  <q-item>
   <q-item-section>
    <q-item-label caption>{{tags.employee.holiday}}:{{empInfo.holiday}}</q-item-label>
    <q-item-label caption>{{tags.employee.weal}}:{{empInfo.weal}}</q-item-label>
    <q-item-label caption>{{tags.employee.sickRatio}}:{{empInfo.sickRatio}}</q-item-label>
   </q-item-section>
   <q-item-section avatar>
    <q-icon name="edit" flat color="primary" @click="ctrl.weal=true"></q-icon>
   </q-item-section>
  </q-item>
</q-list>
<q-list dense v-else>
 <q-item>
  <q-item-section>
    <q-input v-model.number="empInfo.holiday" :label="tags.employee.holiday" type="number"></q-input>
    <q-input v-model.number="empInfo.weal" :label="tags.employee.weal" type="number"></q-input>
    <q-input v-model.number="empInfo.sickRatio" :label="tags.employee.sickRatio" type="number"></q-input>
  </q-item-section>
  <q-item-section avatar>
   <q-btn icon="cancel" @click="ctrl.weal=false" flat color="primary"></q-btn>
   <q-btn icon="done" @click="modifyWeal" flat color="primary"></q-btn>
  </q-item-section>
 </q-item>
</q-list>

<q-separator inset></q-separator>
<q-list dense>
  <q-item>
   <q-item-section>
    <q-item-label caption>{{tags.employee.quali}}:{{empInfo.quali}}</q-item-label>
    <q-item-label caption>{{tags.employee.post}}:{{empInfo.post}}</q-item-label>
    <q-item-label caption>{{tags.employee.subsidy}}:{{empInfo.subsidy}}</q-item-label>
   </q-item-section>
   <q-item-section avatar>
    <q-icon name="grade" flat color="red" @click="showGrade"></q-icon>
   </q-item-section>
  </q-item>
</q-list>

<q-separator inset></q-separator>
<q-list dense>
  <q-item>
   <q-item-section>
    <q-item-label caption>{{tags.employee.salary}}:{{empInfo.salary}}</q-item-label>
    <q-item-label caption>{{tags.employee.dSalary}}:{{empInfo.dSalary}}</q-item-label>
    <q-item-label caption>{{tags.employee.hSalary}}:{{empInfo.hSalary}}</q-item-label>
   </q-item-section>
   <q-item-section avatar>
    <q-icon name="paid" flat color="orange" @click="showSalary"></q-icon>
   </q-item-section>
  </q-item>
</q-list>

<q-separator inset></q-separator>
<q-list dense>
  <q-item>
   <q-item-section>
    <q-item-label caption>{{tags.employee.stock}}:{{empInfo.stock}}</q-item-label>
   </q-item-section>
   <q-item-section avatar>
    <q-icon name="assured_workload" flat color="dark" @click="showStock"></q-icon>
   </q-item-section>
  </q-item>
</q-list>

<q-separator inset></q-separator>
<div class="bg-indigo-1 q-mt-md q-pa-sm">{{tags.employee.manage}}</div>
<div class="q-pa-sm flex flex-center" v-show="workflow.max>1">
 <q-pagination v-model="workflow.cur" color="primary" :max="workflow.max" max-pages="10"
  boundary-numbers="false" @update:model-value="getWorkflows"></q-pagination>
</div>
<q-list dense>
  <q-item v-for="e in workflow.list" clickable @click.stop="showFlow(e.flowid,e.did,e.name)">
   <q-item-section>{{e.dispName}}</q-item-section>
   <q-item-section>{{e.createAt}}</q-item-section>
   <q-item-section side>
    <q-icon :name="e.staIcon" color="blue"></q-icon>
   </q-item-section>
  </q-item>
</q-list>

<div class="bg-indigo-1 q-mt-md q-pa-sm">{{tags.employee.event}}</div>
<div class="q-pa-sm flex flex-center" v-show="event.max>1">
 <q-pagination v-model="event.cur" color="primary" :max="event.max" max-pages="10"
  boundary-numbers="false" @update:model-value="getEvents"></q-pagination>
</div>
<q-list dense>
  <q-item v-for="e in event.list">
   <q-item-section>{{e.type_s}}/{{e.val}}</q-item-section>
   <q-item-section>
    <q-item-label>{{e.cmt}}</q-item-label>
    <q-item-label caption>{{e.at}}</q-item-label>
   </q-item-section>
   <q-item-section side v-if="e.cfmDid<=0">
    <q-btn icon="check_circle" @click="cfmEvent(e.at,e.type)" color="primary" flat></q-btn>
   </q-item-section>
   <q-item-section side v-else>{{e.cfmAcc}}</q-item-section>
  </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="leave.dlg">
 <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{tags.employee.leave}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
     <div class="q-gutter-sm q-pa-sm">
       <q-radio dense v-model="leave.state" val="LEAV" :label="tags.evtType.LEAV"></q-radio>
       <q-radio dense v-model="leave.state" val="DIS" :label="tags.evtType.DIS"></q-radio>
     </div>
     <q-input outlined v-model="leave.cmt" :label="tags.cmt" type="textarea"></q-input>
     <user-input :label="tags.employee.signer" v-model="signer" dense></user-input>
     <q-separator spaced></q-separator>
     <q-list dense>
      <q-item v-for="r in empInfo.rList">
       <q-item-section>
        <q-item-label>{{r.skuName}}</q-item-label>
        <q-item-label caption>{{r.start}}</q-item-label>
       </q-item-section>
       <q-item-section side>
        <q-item-label>{{r.no}}</q-item-label>
        <q-item-label caption>{{r.inDate}}</q-item-label>
       </q-item-section>
      </q-item>
     </q-list>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.ok" color="primary" @click="doLeave" :disable="leave.disable"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="grade.dlg">
 <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{tags.employee.setGrade}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
     <q-input v-model.number="grade.quali" :label="tags.employee.quali" type="number"></q-input>
     <q-input v-model.number="grade.post" :label="tags.employee.post" type="number"></q-input>
     <q-input v-model.number="grade.subsidy" :label="tags.employee.subsidy" type="number"></q-input>
     <q-input outlined v-model="grade.cmt" :label="tags.cmt" type="textarea"></q-input>
     <user-input :label="tags.employee.signer" v-model="signer"></user-input>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.ok" color="primary" @click="modifyGrade"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="stock.dlg">
 <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{tags.employee.setStock}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
     <q-input v-model.number="stock.stock" :label="tags.employee.stock" type="number"></q-input>
     <q-input outlined v-model="stock.cmt" :label="tags.cmt" type="textarea"></q-input>
     <user-input :label="tags.employee.signer" v-model="signer"></user-input>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.ok" color="primary" @click="modifyStock"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="salary.dlg">
 <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{tags.employee.setSalary}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
     <q-input v-model.number="salary.salary" :label="tags.employee.salary"
     @update:model-value="salaryChange" type="number"></q-input>
     <q-input v-model.number="salary.dSalary" :label="tags.employee.dSalary" type="number"></q-input>
     <q-input v-model.number="salary.hSalary" :label="tags.employee.hSalary" type="number"></q-input>
     <q-input outlined v-model="salary.cmt" :label="tags.cmt" type="textarea"></q-input>
     <user-input :label="tags.employee.signer" v-model="signer"></user-input>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.ok" color="primary" @click="modifySalary"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
 </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
`
}