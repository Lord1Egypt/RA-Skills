const EMPTY_ZONE={subsidy:'',salary:'',fowSalary:'',oowSalary:'',wowSalary:'',timeOff:480,name:'',cmt:'',
    taxFunc:'if(s<5000)return 0;\nif(s>5000&&s<=36000)return 0.03*(s-5000);\nreturn 930+(s-36000)*0.1;'};
const EMPTY_SECURITY={name:'',type:'R',sponsor:'C',val:''};
export default {
inject:['service', 'tags'],
data() {return {
    zones:[],
    secs:{}, //劳动保障定义
    secOpts:[],
    edt:{zone:{},security:{}},
    ctrl:{no:-2,zone:-1,tag:'',zoneDlg:false,secDlg:false}
}},
created(){
    this.query_zones();
    for(var i in this.tags.securityTp) {
        this.secOpts.push({label:this.tags.securityTp[i],value:i});
    }
},
methods:{
query_zones(){//查询区域
    var opts={method:"GET", url:"/config/queryZone"}
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            return;
        }
        this.zones=resp.data.list;
        var secs={};
        for(var z of resp.data.list) {
            secs[z.id]=[]; //全部加一个空社保，避免未设置社保的secs为空，添加时抛异常
        }
        var props=this.tags.securityProp;
        var names=this.tags.securityTp;
        var zoneSec;
        for(var s of resp.data.secs) {
            s.name_s=names[s.name]?names[s.name]:s.name;
            s.sponsor_s=props[s.sponsor];
            s.type_s=props[s.type];
            zoneSec=secs[s.zone];
            if(zoneSec) {
                zoneSec.push(s);
            }
        }
        this.secs=secs;
    })  
},
show_zone(i) {
    if(i>-1) {
        this.ctrl.tag=this.tags.modify;
        this.edt.zone.id=this.zones[i].id;
        copyObjTo(this.zones[i], this.edt.zone);
    } else {
        this.ctrl.tag=this.tags.add;
        copyObjTo(EMPTY_ZONE, this.edt.zone);
    }
    this.ctrl.tag+=this.tags.cfg.zone;
    this.ctrl.no=i;
    this.ctrl.zoneDlg=true;
},
zone_do() {
    var opts;
    if(this.ctrl.no>-1) {
        opts={method:"PUT",url:"/config/updateZone",data:this.edt.zone};
    } else {
        opts={method:"POST",url:"/config/addZone",data:this.edt.zone};
    }
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        if(this.ctrl.no>-1) {
            copyObjTo(this.edt.zone, this.zones[this.ctrl.no]);
        } else {
            var zone = {id:resp.data.id};
            copyObjTo(this.edt.zone, zone);
            this.secs[zone.id]=[];
            this.zones.push(zone);
        }
        this.ctrl.no=-2;
        this.ctrl.zoneDlg=false;
    });
},
remove_zone() {
    var i=this.ctrl.no;
    var opts={method:"DELETE",url:"/config/removeZone?id="+this.zones[i].id};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.zones.splice(i,1);
        this.ctrl.no=-2;
        this.ctrl.zoneDlg=false;
    });
},
show_security(zone,i) {
    if(i<0) {
        this.ctrl.tag=this.tags.add;
        copyObjTo(EMPTY_SECURITY, this.edt.security);
        this.edt.security.zone=zone;
    } else {
        this.ctrl.tag=this.tags.modify;
        copyObjTo(this.secs[zone][i], this.edt.security);
    }
    this.ctrl.tag+=this.tags.cfg.security;
    this.ctrl.no=i;
    this.ctrl.zone=zone;
    this.ctrl.secDlg=true;
},
security_do() {
    var opts;
    if(this.ctrl.no>-1) {
        opts={method:"PUT",url:"/config/updateSecurity",data:this.edt.security};
    } else {
        opts={method:"POST",url:"/config/addSecurity",data:this.edt.security};
    }
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        var props=this.tags.securityProp;
        var names=this.tags.securityTp;
        var security=cloneObj(this.edt.security);
        var secs=this.secs[security.zone];
        security.name_s=names[security.name]?names[security.name]:security.name;
        security.sponsor_s=props[security.sponsor];
        security.type_s=props[security.type];
        if(this.ctrl.no>-1) {
            copyObjTo(security, secs[this.ctrl.no]);
        } else {
            secs.push(security);
        }
        this.ctrl.no=-2;
        this.ctrl.secDlg=false;
    });
    
},
remove_security() {
    var i=this.ctrl.no;
    var zone=this.ctrl.zone;
    var sec=this.secs[zone][i];
    var url="/config/removeSecurity?zone="+zone+"&sponsor="+sec.sponsor+"&name="+sec.name;
    var opts={method:"DELETE",url:url};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.secs[zone].splice(i,1);
        this.ctrl.no=-2;
        this.ctrl.secDlg=false;
    });
},
add_sec_opt(val, done) {
    if (val.length > 2) {
      if (!this.tags.securityTp[val]) {
        done(val, 'add-unique');
      }
    }
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat round icon="arrow_back" dense @click="service.back()"></q-btn>
     <q-toolbar-title>{{tags.cfg.zone}}</q-toolbar-title>
     <q-btn icon="add_circle" @click="show_zone(-1)" flat dense></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-none">
<q-list v-for="(z,i) in zones" dense>
 <q-item clickable @click="show_zone(i)">
  <q-item-section>
   <q-item-label class="text-h5">{{z.name}}</q-item-label>
   <q-item-label caption>{{tags.cfg.timeOff}}:{{z.timeOff}}</q-item-label>
   <q-item-label caption>{{z.cmt}}</q-item-label>
  </q-item-section>
  <q-item-section>
   <q-item-label caption>{{tags.cfg.salary}}:{{z.salary}}</q-item-label>
   <q-item-label caption>{{tags.cfg.wowSalary}}:{{z.wowSalary}}<q-item-label>
   <q-item-label caption>{{tags.cfg.oowSalary}}:{{z.oowSalary}}<q-item-label>
   <q-item-label caption>{{tags.cfg.fowSalary}}:{{z.fowSalary}}<q-item-label>
   <q-item-label caption>{{tags.cfg.subsidy}}:{{z.subsidy}}</q-item-label>
  </q-item-section>
 </q-item>
 <q-item>
  <q-item-section class="text-teal">{{tags.cfg.security}}</q-item-section>
  <q-item-section>
   <q-icon @click="show_security(z.id,-1)" name='add_circle' color="primary" flat size="1.5em"></q-icon>
  </q-item-section>
 </q-item>
 <q-item v-for="(s,i) in secs[z.id]" clickable @click="show_security(z.id,i)">
  <q-item-section><q-item-label caption>{{s.name_s}}({{s.sponsor_s}})</q-item-label></q-item-section>
  <q-item-section>
   <q-item-label caption>{{s.val}}({{s.type_s}})</q-item-label>
  </q-item-section>
 </q-item>
 <q-separator spaced></q-separator>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="ctrl.zoneDlg" persistent>
 <q-card style="min-width:70vw">
  <q-card-section>
    <div class="text-h6">{{ctrl.tag}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-input :label="tags.name" v-model="edt.zone.name" dense></q-input>
   <q-input :label="tags.cfg.salary" v-model.number="edt.zone.salary" dense type="number"></q-input>
   <q-input :label="tags.cfg.wowSalary" v-model.number="edt.zone.wowSalary" dense type="number"></q-input>
   <q-input :label="tags.cfg.oowSalary" v-model.number="edt.zone.oowSalary" dense type="number"></q-input>
   <q-input :label="tags.cfg.fowSalary" v-model.number="edt.zone.fowSalary" dense type="number"></q-input>
   <q-input :label="tags.cfg.subsidy" v-model.number="edt.zone.subsidy" dense type="number"></q-input>
   <q-input :label="tags.cfg.timeOff" v-model.number="edt.zone.timeOff" dense type="number"></q-input>
   <q-input :label="tags.cfg.taxFunc" v-model="edt.zone.taxFunc" dense type="textarea"></q-input>
   <q-input :label="tags.cmt" v-model="edt.zone.cmt" dense type="textarea" rows="2"></q-input>
  </q-card-section>
  <q-card-actions class="row">
   <div class="col" v-if="ctrl.no>-1">
    <q-btn :label="tags.remove" flat color="red" @click="remove_zone()"></q-btn>
   </div>
   <div class="col text-right">
    <q-btn :label="tags.ok" color="primary" @click="zone_do"></q-btn>
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
   </div>
  </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="ctrl.secDlg" persistent>
 <q-card style="min-width:70vw">
  <q-card-section>
    <div class="text-h6">{{ctrl.tag}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-select v-model="edt.security.name" use-input @new-value="add_sec_opt"
    :options="secOpts" :label="tags.name" dense map-options emit-value></q-select>
   <div class="q-gutter-sm">
     <q-radio v-model="edt.security.sponsor"
      val="C" :label="tags.securityProp['C']"></q-radio>
     <q-radio v-model="edt.security.sponsor"
      val="P" :label="tags.securityProp['P']"></q-radio>
   </div>
   <div class="q-gutter-sm">
    <q-radio v-model="edt.security.type"
     val="R" :label="tags.securityProp['R']"></q-radio>
    <q-radio v-model="edt.security.type"
     val="V" :label="tags.securityProp['V']"></q-radio>
   </div>
   <q-input :label="tags.val" v-model.number="edt.security.val" dense type="number"></q-input>
  </q-card-section>
  <q-card-actions class="row">
   <div class="col" v-if="ctrl.no>-1">
    <q-btn :label="tags.remove" flat color="red" @click="remove_security()"></q-btn>
   </div>
   <div class="col text-right">
    <q-btn :label="tags.ok" color="primary" @click="security_do"></q-btn>
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
   </div>
  </q-card-actions>
 </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
`
}