import {sta2icon} from '/assets/v3/components/workflow.js';
export default {
inject:['service', 'tags'],
data() {return {
    uid:this.$route.query.uid,
    perInfo:{}, //人才信息
    contacts:[], //联系记录
    empInfo:{uid:this.$route.query.uid,
        office:'',worktime:0,quali:'',post:'',
        salary:'',dSalary:'',hSalary:'',subsidy:'',entryAt:'',
        account:'',addr:'',email:'',idno:'', signer:''},
    ctrl:{fun:'',pi:{},entryDlg:false,cntDlg:false},
    contact:{dlg:false, type:'',act:'',cmt:'',at:'',uid:this.$route.query.uid,tag:''},
    opts:{edu:[],state:[],zone:[],office:[],worktime:[],marriage:[]},
    userInput:{id:-1,account:''}
}},
created(){
    this.get();
    var eOpts=[];
    for(var i in this.tags.edu) {
        eOpts.push({value:i,label:this.tags.edu[i]});
    }
    this.opts.edu=eOpts;
    
    var sOpts=[];
    for(var i in this.tags.perState) {
        if(i=='JOIN') continue;
        sOpts.push({value:i,label:this.tags.perState[i]});
    }
    this.opts.state=sOpts;
    this.service.worktimeList().then(opts=>{
        this.opts.worktime=opts;
    });
    this.service.zoneList().then(opts=>{
        this.opts.zone=opts;
    });
    var opts=[];
    for(var i in this.tags.marriageSta) {
        opts.push({value:i,label:this.tags.marriageSta[i]});
    }
    this.opts.marriage=opts;
    this.getContacts();
},
methods:{
get() {
    var url = "/api/pool/get?uid="+this.uid;
    request({method:"GET",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            return;
        }
        this.convert(resp.data, this.perInfo);
    })
},
convert(src, p) {
    var dt=new Date();
    var year=dt.getFullYear();
    copyObjTo(src, p);
    p.uid=this.uid;
    p.sex_s=this.tags.sex[p.sex];
    p.state_s=this.tags.perState[p.state];
    p.joinable=p.state!='PROC'&&p.state!='JOIN';
    p.maxEdu_s=this.tags.edu[p.maxEdu];
    p.firstEdu_s=this.tags.edu[p.firstEdu];
    p.marriage_s=this.tags.marriageSta[p.marriage];
    dt.setTime(p.birth*60000);
    p.age=year-dt.getFullYear();
    p.birth_s=date2str(dt);
    dt.setTime(p.createAt*60000);
    p.createAt_s=date2str(dt);
    dt.setTime(p.update_time);
    p.updateAt=date2str(dt);
    if(src.entry) {
        p.entry.staIcon=sta2icon(src.entry.status);
        dt.setTime(src.entry.createAt*60000);
        p.entry.createAt=date2str(dt);
    }
},
showModify() {
    this.ctrl.pi=copyObjExc(this.perInfo, ['state']);
    this.ctrl.fun='modify';
},
remove() {
    request({method:"DELETE",url:"/api/pool/remove?uid="+this.perInfo.uid}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.service.back();
    });
},
modify() {
    var url="/api/pool/update";
    this.ctrl.pi.birth=parseInt(new Date(this.ctrl.pi.birth_s).getTime()/60000);
    var dta=copyObjExc(this.ctrl.pi, ['entry']);

    request({method:"PUT",url:url,data:dta}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.convert(dta, this.perInfo);
        this.ctrl.fun='';
    });
},
doEntry() {
    var url="/api/wfemployee/entry";
    var dta=copyObjExc(this.empInfo,['entryAt']);
    dta.signer=this.userInput.account;
    dta.entryAt=parseInt(new Date(this.empInfo.entryAt).getTime()/60000);
    request({method:"POST",url:url,data:dta}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.ctrl.entryDlg=false;
        this.get();
    });
},
changeOffice(zone) {
    this.service.officeList(zone).then(opts=>{
        if(opts&&opts.length>0) {
            this.opts.office=opts;
            this.empInfo.office=opts[0].value;
        } else {
            this.opts.office=[];
            this.empInfo.office='';
        }
    });
},
salaryChange(v) {
    this.empInfo.dSalary=parseInt(v/22);
    this.empInfo.hSalary=parseInt(v/(22*8));
},
//联系记录操作
getContacts() {
    var url = "/api/pool/listContact?uid="+this.uid;
    request({method:"GET",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            return;
        }
        var dt=new Date();
        var list=[];
        for(var e of resp.data.list) {
            dt.setTime(e.at*60000);
            e.at_s=date2str(dt);
            e.act_s=this.tags.perState[e.act];
            list.push(e);
        }
        this.contacts=list;
    })
},
showCntDlg(type,i) {
    if(type=='add') {
        this.contact.tag=this.tags.add;
        this.contact.cmt='';
        this.contact.act='CONT';
        this.contact.at_s=date2str(new Date());
    } else {
        this.contact.tag=this.tags.modify;
        var c=this.contacts[i];
        this.contact.act=c.act;
        this.contact.cmt=c.cmt;
        this.contact.at_s=c.at_s;
    }
    this.contact.type=type;
    this.contact.dlg=true;
},
doContactAct() {
    var vPromize;
    var dta={uid:this.uid, cmt:this.contact.cmt, act:this.contact.act};
    dta.at=parseInt(new Date(this.contact.at_s).getTime()/60000);
    if(this.contact.type=='add') {
        vPromize = request({method:"POST",url:"/api/pool/addContact",data:dta}, this.service.name);
    } else {
        vPromize = request({method:"PUT",url:"/api/pool/updateContact",data:dta}, this.service.name);
    }
    vPromize.then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.contact.dlg=false;
        this.getContacts();
    });
},
showEntry() {
    var e=this.perInfo.entry;
    var url='/workflow?flow='+e.flowid+"&did="+e.did+"&type=entry";
    this.service.goto(url);
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat icon="arrow_back" dense @click="service.back"></q-btn>
    <q-toolbar-title>{{tags.pool.detail}}-{{perInfo.name}} {{perInfo.sex_s}}</q-toolbar-title>
    <q-btn icon="delete" @click="remove" v-show="perInfo.state=='DISC'" flat></q-btn>
    <q-btn icon="edit" @click="showModify" v-show="ctrl.fun==''" flat></q-btn>
    <q-btn :label="tags.employee.join" @click="ctrl.entryDlg=true" v-if="perInfo.joinable" flat></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
<div v-show="ctrl.fun==''">
 <q-list dense>
  <q-item>
   <q-item-section>{{tags.pool.state}}</q-item-section>
   <q-item-section side>{{perInfo.state_s}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.employee.maxEdu}}</q-item-section>
   <q-item-section side>{{perInfo.maxEdu_s}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.employee.firstEdu}}</q-item-section>
   <q-item-section side>{{perInfo.firstEdu_s}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.employee.quali}}</q-item-section>
   <q-item-section side>{{perInfo.quali}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.pool.expSalary}}</q-item-section>
   <q-item-section side>{{perInfo.expSalary}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.pub.phone}}</q-item-section>
   <q-item-section side>{{perInfo.phone}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.pub.email}}</q-item-section>
   <q-item-section side>{{perInfo.email}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.pub.birth}}</q-item-section>
   <q-item-section side>{{perInfo.birth_s}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.pool.marriage}}</q-item-section>
   <q-item-section side>{{perInfo.marriage_s}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.pool.cmt}}</q-item-section>
   <q-item-section side>{{perInfo.cmt}}</q-item-section>
  </q-item>
  <q-item clickable @click="showEntry" v-if="perInfo.entry">
   <q-item-section class="text-blue">{{perInfo.entry.dispName}}</q-item-section>
   <q-item-section side>
    <q-item-label><q-icon :name="perInfo.entry.staIcon" color="blue"></q-icon></q-item-label>
    <q-item-label caption class="text-blue">{{perInfo.entry.createAt}}</q-item-label>
   </q-item-section>
  </q-item>
 </q-list>
</div>
<div v-show="ctrl.fun=='modify'">
 <q-list dense>
  <q-item>
   <q-item-section>{{tags.pool.state}}</q-item-section>
   <q-item-section side>{{perInfo.state_s}}</q-item-section>
  </q-item>
  <q-item><q-item-section>
   <q-input v-model="ctrl.pi.name" :label="tags.pool.name" dense maxlength=80>
    <template v-slot:after>
     <q-radio v-model="ctrl.pi.sex" class="text-caption"
     v-for="(s,v) in tags.sex" :val="v" :label="s"></q-radio>
    </template>
   </q-input>
  </q-item-section></q-item>
  <q-item><q-item-section>
   <q-select v-model="ctrl.pi.maxEdu" :label="tags.employee.maxEdu"
    :options="opts.edu" emit-value dense map-options></q-select>
  </q-item-section></q-item>
  <q-item><q-item-section>
   <q-select v-model="ctrl.pi.firstEdu" :label="tags.employee.firstEdu"
    :options="opts.edu" emit-value dense map-options></q-select>
  </q-item-section></q-item>
  <q-item><q-item-section>
   <q-input v-model.number="ctrl.pi.quali" :label="tags.employee.quali" dense type="number"></q-input>
  </q-item-section></q-item>
  <q-item><q-item-section>
   <q-input v-model.number="ctrl.pi.expSalary" :label="tags.pool.expSalary" dense type="number"></q-input>
  </q-item-section></q-item>
  <q-item><q-item-section>
   <q-input v-model.number="ctrl.pi.phone" :label="tags.pool.phone" dense maxlength=90 type="number"></q-input>
  </q-item-section></q-item>
  <q-item><q-item-section>
   <date-input v-model="ctrl.pi.birth_s" :label="tags.pool.birth"
    :close="tags.ok" max="today"></date-input>
  </q-item-section></q-item>
  <q-item><q-item-section>
   <q-select v-model="ctrl.pi.marriage" :options="opts.marriage" emit-value
    :label="tags.pool.marriage" dense map-options></q-select>
  </q-item-section></q-item>
  <q-item><q-item-section>
   <q-input v-model="ctrl.pi.email" :label="tags.pub.email" dense maxlength=80></q-input>
  </q-item-section></q-item>
  <q-item><q-item-section>
   <q-input v-model="ctrl.pi.cmt" :label="tags.pool.cmt" dense maxlength=500></q-input>
  </q-item-section></q-item>
 </q-list>
 <div class="text-right">
   <q-btn flat :label="tags.cancel" color="primary" @click="ctrl.fun=''"></q-btn>
   <q-btn icon="done" :label="tags.ok" color="primary" @click="modify"></q-btn>
 </div>
</div>

<q-separator inset></q-separator>
<q-banner inline-actions class="bg-indigo-1 q-ma-sm" dense>
  {{tags.pool.contact}}
  <template v-slot:action>
   <q-icon flat color="primary" name="add_circle" @click.stop="showCntDlg('add')"></q-icon>
  </template>
</q-banner>
<q-list dense>
  <q-item v-for="(c,i) in contacts" clickable @click="showCntDlg('edit',i)">
   <q-item-section avatar>{{c.account}}</q-item-section>
   <q-item-section>{{c.cmt}}</q-item-section>
   <q-item-section side>{{c.act_s}}/{{c.at_s}}</q-item-section>
  </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="contact.dlg" persistent>
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{contact.tag}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
     <div class="q-gutter-sm">
      <q-radio v-model="contact.act" val="CONT" :label="tags.perState.CONT"></q-radio>
      <q-radio v-model="contact.act" val="EXAM" :label="tags.perState.EXAM"></q-radio>
      <q-radio v-model="contact.act" val="REJ" :label="tags.perState.REJ"></q-radio>
      <q-radio v-model="contact.act" val="DISC" :label="tags.perState.DISC"></q-radio>
     </div>
     <div v-if="contact.type=='edit'">{{contact.at_s}}</div>
     <date-input v-else :close="tags.ok" :label="tags.pool.at" v-model="contact.at_s" max="today"></date-input>
     <q-input v-model="contact.cmt" :label="tags.cmt" type="textarea" maxlength="85"></q-input>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.ok" color="primary" @click="doContactAct()"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<q-dialog v-model="ctrl.entryDlg" persistent>
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{tags.employee.join}}({{perInfo.name}}/{{perInfo.phone}})</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
     <q-list>
      <q-item><q-item-section>
       <q-input v-model.number="empInfo.account" :label="tags.pub.account" dense type="number"></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <div class="row">
        <div class="col">
         <q-input v-model.number="empInfo.quali" :label="tags.employee.quali" dense type="number"></q-input>
        </div>
        <div class="col">
         <q-input v-model.number="empInfo.post" :label="tags.employee.post" dense type="number"></q-input>
        </div>
        <div class="col">
         <q-input v-model.number="empInfo.subsidy" :label="tags.employee.subsidy" dense type="number"></q-input>
        </div>
       </div>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <div class="row">
        <div class="col">
         <q-select v-model="empInfo.zone" :options="opts.zone" emit-value
         @update:model-value="changeOffice"
         :label="tags.employee.zone" dense map-options></q-select>
        </div>
        <div class="col">
         <q-select v-model="empInfo.office" :options="opts.office" emit-value
         :label="tags.employee.office" dense map-options></q-select>
        </div>
        <div class="col">
         <q-select v-model="empInfo.worktime" :options="opts.worktime" emit-value
          :label="tags.employee.worktime" dense map-options></q-select>
        </div>
       </div>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <div class="row">
        <div class="col">
         <q-input v-model.number="empInfo.salary" :label="tags.employee.salary"
         @update:model-value="salaryChange" dense type="number"></q-input>
        </div>
        <div class="col">
         <q-input v-model.number="empInfo.dSalary" :label="tags.employee.dSalary" dense type="number"></q-input>
        </div>
        <div class="col">
         <q-input v-model.number="empInfo.hSalary" :label="tags.employee.hSalary" dense type="number"></q-input>
        </div>
       </div>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-input v-model="empInfo.idno" :label="tags.employee.idno" dense maxlength=18></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-input v-model="empInfo.email" :label="tags.employee.email" dense maxlength=80></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-input v-model="empInfo.addr" :label="tags.employee.addr" dense maxlength=80></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <date-input v-model="empInfo.entryAt" :label="tags.employee.entryAt"
        :close="tags.ok"></date-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <user-input :label="tags.employee.signer" v-model="userInput"></user-input>
      </q-item-section></q-item>
     </q-list>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.ok" color="primary" @click="doEntry"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
`
}